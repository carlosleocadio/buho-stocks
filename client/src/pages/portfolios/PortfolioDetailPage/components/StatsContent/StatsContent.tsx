/* eslint-disable react/jsx-props-no-spreading */
import React, { ReactElement } from "react";
import { useTranslation } from "react-i18next";
import { ArrowDownOutlined, ArrowUpOutlined } from "@ant-design/icons";
import { Col, Row, Statistic, Typography } from "antd";

interface Props {
  stats: any;
}

export default function StatsContent({ stats }: Props): ReactElement {
  const { t } = useTranslation();

  const columnProps = {
    xs: { span: 12 },
    lg: { span: 6 },
  };

  return (
    <Row gutter={24} style={{ marginTop: 16 }}>
      <Col {...columnProps}>
        <Statistic
          title={`${t("Invested")}`}
          value={stats?.invested}
          precision={2}
          suffix={stats?.portfolioCurrency}
        />
      </Col>
      <Col {...columnProps}>
        <Statistic
          title={`${t("Accum. investment")}`}
          value={stats?.accumulatedInvestment}
          precision={2}
          suffix={stats?.portfolioCurrency}
        />
      </Col>
      <Col {...columnProps}>
        <Statistic
          title={`${t("Portfolio value")}`}
          value={stats?.portfolioValue}
          valueStyle={{
            color:
              Number(stats?.portfolioValue) <
              Number(stats?.accumulatedInvestment)
                ? "#cf1322"
                : "",
          }}
          precision={2}
          suffix={stats?.portfolioCurrency}
        />
      </Col>
      <Col {...columnProps}>
        <Statistic
          title={`${t("Dividends")}`}
          value={stats?.dividends}
          precision={2}
          suffix={stats?.portfolioCurrency}
        />
      </Col>
      <Col {...columnProps}>
        <Statistic
          title={`${t("Accum. Dividends")}`}
          value={stats?.accumulatedDividends}
          precision={2}
          suffix={stats?.portfolioCurrency}
        />
      </Col>
      <Col {...columnProps}>
        <Statistic
          title={`${t("Dividends yield")}`}
          value={stats?.dividendsYield}
          precision={2}
          suffix="%"
        />
      </Col>
      <Col {...columnProps}>
        <Statistic
          title={`${t("Return")}`}
          value={stats?.returnValue}
          precision={2}
          suffix={stats?.portfolioCurrency}
        />
        <Typography.Text type={stats?.returnPercent < 0 ? "danger" : "success"}>
          {stats?.returnValue < 0 ? <ArrowDownOutlined /> : <ArrowUpOutlined />}
          {stats?.returnPercent ? Number(stats.returnPercent).toFixed(2) : ""}%
        </Typography.Text>
      </Col>
      <Col {...columnProps}>
        <Statistic
          title={`${t("Return + dividends")}`}
          value={stats?.returnWithDividends}
          precision={2}
          valueStyle={{
            color: stats?.returnWithDividends < 0 ? "#cf1322" : "",
          }}
          suffix={stats?.portfolioCurrency}
        />
        <Typography.Text
          type={stats?.returnWithDividendsPercent < 0 ? "danger" : "success"}
        >
          {stats?.returnWithDividends < 0 ? (
            <ArrowDownOutlined />
          ) : (
            <ArrowUpOutlined />
          )}{" "}
          {stats?.returnWithDividendsPercent
            ? Number(stats.returnWithDividendsPercent).toFixed(2)
            : ""}
          %
        </Typography.Text>
      </Col>
    </Row>
  );
}
