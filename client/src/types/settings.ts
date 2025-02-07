export interface ISettingsFormFields {
  language: string;
  companySortBy: string;
  companyDisplayMode: string;
  mainPortfolio: string;
  portfolioSortBy: string;
  portfolioDisplayMode: string;
  timezone: string;
}

export interface ISettings extends ISettingsFormFields {
  id: number;
  allowFetch: boolean;
  dateCreated: string;
  lastUpdated: string;
}
