import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  Alert,
  Button,
  Col,
  DatePicker,
  Form,
  Input,
  InputNumber,
  Modal,
  Row,
} from "antd";
// eslint-disable-next-line import/no-extraneous-dependencies
import moment from "moment";
import LoadingSpin from "components/LoadingSpin/LoadingSpin";
import {
  useAddDividendsTransaction,
  useDividendsTransaction,
  useUpdateDividendsTransaction,
} from "hooks/use-dividends-transactions/use-dividends-transactions";
import { useExchangeRate } from "hooks/use-exchange-rates/use-exchange-rates";
import { ICurrency } from "types/currency";
import { IDividendsTransactionFormFields } from "types/dividends-transaction";

interface IProps {
  transactionId?: number;
  companyId: number;
  companyDividendsCurrency: ICurrency;
  portfolioBaseCurrency: string;
  title: string;
  okText: string;
  isModalVisible: boolean;
  onCreate: (values: any) => void;
  onCancel: () => void;
}

export default function DividendsTransactionAddEditForm({
  transactionId,
  companyId,
  companyDividendsCurrency,
  portfolioBaseCurrency,
  title,
  okText,
  isModalVisible,
  onCreate,
  onCancel,
}: IProps) {
  const [form] = Form.useForm();
  const { t } = useTranslation();

  const dateFormat = "YYYY-MM-DD";
  const [currentTransactionDate, setCurrentTransactionDate] = useState<string>(
    moment(new Date()).format(dateFormat),
  );

  const { isFetching: exchangeRateLoading, refetch } = useExchangeRate(
    companyDividendsCurrency.code,
    portfolioBaseCurrency,
    currentTransactionDate,
  );
  const { mutate: updateTransaction, isLoading: isLoadingUpdate } =
    useUpdateDividendsTransaction();
  const { mutate: createTransaction, isLoading: isLoadindCreate } =
    useAddDividendsTransaction();
  const {
    data: transaction,
    error: errorFetchingTransaction,
    isFetching,
    isSuccess,
  } = useDividendsTransaction(companyId, transactionId);

  const fetchExchangeRate = async () => {
    const { data: exchangeRateResult } = await refetch();
    if (exchangeRateResult) {
      form.setFieldsValue({
        exchangeRate: exchangeRateResult.exchangeRate,
      });
    } else {
      form.setFields([
        {
          name: "exchangeRate",
          errors: [t("Unable to fetch the exchange rates for the given date")],
        },
      ]);
    }
  };

  const handleSubmit = async (values: any) => {
    const {
      count,
      grossPricePerShare,
      totalCommission,
      exchangeRate: exchangeRateValue,
      notes,
    } = values;

    const newTransactionValues: IDividendsTransactionFormFields = {
      count,
      grossPricePerShare,
      grossPricePerShareCurrency: companyDividendsCurrency.code,
      totalCommission,
      totalCommissionCurrency: companyDividendsCurrency.code,
      transactionDate: currentTransactionDate,
      notes,
      exchangeRate: exchangeRateValue ? +exchangeRateValue : 1,
      company: +companyId!,
      color: "#000",
    };
    if (transactionId) {
      updateTransaction({
        companyId: +companyId!,
        transactionId,
        newTransaction: newTransactionValues,
      });
    } else {
      createTransaction({
        companyId: +companyId!,
        newTransaction: newTransactionValues,
      });
    }
  };

  const currentTransactionDateChange = (
    value: moment.Moment | null,
    dateString: string,
  ) => {
    setCurrentTransactionDate(dateString);
  };

  const handleFormSubmit = async () => {
    try {
      const values = await form.validateFields();
      await handleSubmit(values);
      form.resetFields();
      onCreate(values);
    } catch (error) {
      console.log("Validate Failed:", error);
    }
  };

  useEffect(() => {
    if (transaction) {
      form.setFieldsValue({
        count: transaction.count,
        grossPricePerShare: transaction.grossPricePerShare,
        totalCommission: transaction.totalCommission,
        exchangeRate: transaction.exchangeRate,
        notes: transaction.notes,
        transactionDate: moment(transaction.transactionDate),
      });
      setCurrentTransactionDate(transaction.transactionDate);
    }
  }, [form, transaction]);

  return (
    <Modal
      visible={isModalVisible}
      title={title}
      okText={okText}
      cancelText={t("Cancel")}
      onCancel={onCancel}
      onOk={handleFormSubmit}
      confirmLoading={isLoadingUpdate || isLoadindCreate}
    >
      {isFetching && <LoadingSpin />}
      {errorFetchingTransaction && (
        <Alert
          showIcon
          message={t("Unable to load transaction")}
          description={errorFetchingTransaction.message}
          type="error"
        />
      )}
      {(isSuccess || !transactionId) && (
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item
            name="count"
            label={t("Number of shares")}
            rules={[
              {
                required: true,
                message: t("Please input the number of shares"),
              },
            ]}
          >
            <InputNumber min={0} step={1} style={{ width: "100%" }} />
          </Form.Item>
          <Form.Item
            name="grossPricePerShare"
            label={t("Gross price per share")}
            rules={[
              {
                required: true,
                message: t("Please input the gross price per share"),
              },
            ]}
          >
            <InputNumber
              decimalSeparator="."
              addonAfter={`${companyDividendsCurrency.code}`}
              min={0}
              step={0.001}
            />
          </Form.Item>

          <Form.Item
            name="totalCommission"
            label={t("Total commission")}
            rules={[
              {
                required: true,
                message: t("Please input the total commission"),
              },
            ]}
          >
            <InputNumber
              addonAfter={`${companyDividendsCurrency.code}`}
              decimalSeparator="."
              min={0}
              step={0.001}
            />
          </Form.Item>
          <Form.Item
            name="transactionDate"
            label={t("Transaction's date")}
            rules={[
              {
                required: true,
                message: t("Please input the date of the operation"),
              },
            ]}
          >
            <DatePicker
              format={dateFormat}
              onChange={currentTransactionDateChange}
            />
          </Form.Item>
          {companyDividendsCurrency.code !== portfolioBaseCurrency && (
            <Row gutter={8}>
              <Col span={12}>
                <Form.Item
                  name="exchangeRate"
                  label={t("Exchange rate")}
                  rules={[
                    {
                      required: true,
                      message: t("Please input the exchange rate"),
                    },
                  ]}
                  help={`${companyDividendsCurrency.code} ${t("to")}
                  ${portfolioBaseCurrency}`}
                >
                  <InputNumber
                    decimalSeparator="."
                    min={0}
                    step={0.001}
                    style={{ width: "100%" }}
                    disabled={exchangeRateLoading}
                  />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item label="&nbsp;">
                  <Button
                    disabled={currentTransactionDate === null}
                    onClick={fetchExchangeRate}
                    loading={exchangeRateLoading}
                  >
                    {t("Get exchange rate")}
                  </Button>
                </Form.Item>
              </Col>
            </Row>
          )}

          <Form.Item name="notes" label={t("Notes")}>
            <Input.TextArea rows={4} />
          </Form.Item>
        </Form>
      )}
    </Modal>
  );
}

DividendsTransactionAddEditForm.defaultProps = {
  transactionId: undefined,
};
