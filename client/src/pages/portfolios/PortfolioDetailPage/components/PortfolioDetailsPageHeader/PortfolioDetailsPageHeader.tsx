import React, { ReactNode, useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate, useParams } from "react-router-dom";
import {
  DeleteOutlined,
  LineChartOutlined,
  PlusOutlined,
  UnorderedListOutlined,
} from "@ant-design/icons";
import { Button, PageHeader, Popconfirm } from "antd";
import breadCrumbRender from "breadcrumbs";
import CountryFlag from "components/CountryFlag/CountryFlag";
import { useDeletePortfolio } from "hooks/use-portfolios/use-portfolios";
import CompanyAddEditForm from "pages/companies/CompanyDetailsPage/components/CompanyAddEditForm/CompanyAddEditForm";

interface Props {
  portfolioName: string;
  portfolioDescription: string;
  portfolioCountryCode: string;
  children?: ReactNode;
}

function PortfolioDetailsPageHeader({
  portfolioName,
  portfolioDescription,
  portfolioCountryCode,
  children,
}: Props) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { id } = useParams();
  const { mutate: deletePortfolio } = useDeletePortfolio();
  const routes = [
    {
      path: `/app/portfolios/${id}`,
      breadcrumbName: portfolioName,
    },
  ];
  const [isModalVisible, setIsModalVisible] = useState(false);

  const showModal = () => {
    setIsModalVisible(true);
  };

  const onCreate = (values: any) => {
    console.log("Received values of form: ", values);
    setIsModalVisible(false);
  };

  const onCancel = () => {
    setIsModalVisible(false);
  };

  const confirmDelete = async () => {
    deletePortfolio({ portfolioId: +id! });
    navigate(-1);
  };

  return (
    <PageHeader
      className="site-page-header"
      title={portfolioName}
      subTitle={portfolioDescription}
      breadcrumb={{ routes }}
      breadcrumbRender={breadCrumbRender}
      tags={[
        <CountryFlag code={portfolioCountryCode} key={portfolioCountryCode} />,
      ]}
      extra={[
        <Button
          key="company-view-logs"
          icon={<UnorderedListOutlined />}
          onClick={() => {
            navigate(`log`);
          }}
          title={t("View portfolio logs")}
        />,
        <Button
          key="company-view-charts"
          icon={<LineChartOutlined />}
          onClick={() => {
            navigate(`charts`);
          }}
          title={t("View portfolio charts")}
        />,
        <Button
          type="primary"
          key="company-add-header"
          icon={<PlusOutlined />}
          onClick={showModal}
        >
          {t("Company")}
        </Button>,
        <Popconfirm
          key="portfolio-delete-header"
          title="Delete this portfolio?"
          onConfirm={() => confirmDelete()}
          okText={t("Yes")}
          cancelText={t("No")}
        >
          <Button icon={<DeleteOutlined />} danger>
            {t("Delete")}
          </Button>
        </Popconfirm>,
      ]}
    >
      {children}
      <CompanyAddEditForm
        title={t("Add new company")}
        okText={t("Create")}
        portfolioId={+id!}
        isModalVisible={isModalVisible}
        onCreate={onCreate}
        onCancel={onCancel}
      />
    </PageHeader>
  );
}
PortfolioDetailsPageHeader.defaultProps = {
  children: null,
};
export default PortfolioDetailsPageHeader;
