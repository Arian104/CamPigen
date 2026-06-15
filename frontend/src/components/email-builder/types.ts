export type EmailBlockType =
  | "hero"
  | "text"
  | "button"
  | "image"
  | "divider"
  | "footer"
  | "spacer"
  | "card"
  | "coupon"
  | "social"
  | "product";

export type EmailBlock = {
  id: string;
  type: EmailBlockType;
  span: 1 | 2 | 3;
  props: Record<string, string>;
};

export type EmailBuilderSchema = {
  columns: 3;
  blocks: EmailBlock[];
};

export const DEFAULT_SCHEMA: EmailBuilderSchema = {
  columns: 3,
  blocks: [
    {
      id: "hero_1",
      type: "hero",
      span: 3,
      props: {
        title: "Hello {{ first_name }}",
        subtitle: "Welcome to {{ company_name }}",
        buttonText: "Get Started",
        buttonUrl: "{{ dashboard_url }}",
        backgroundColor: "#111827",
        textColor: "#ffffff",
        subTextColor: "#d1d5db",
        buttonBackgroundColor: "#ffffff",
        buttonTextColor: "#111827",
      },
    },
    {
      id: "text_1",
      type: "text",
      span: 3,
      props: {
        content: "Use this section to explain your offer or announcement.",
        backgroundColor: "#ffffff",
        textColor: "#374151",
      },
    },
    {
      id: "card_1",
      type: "card",
      span: 1,
      props: {
        title: "Fast Delivery",
        content: "Send emails through your SMTP infrastructure.",
        backgroundColor: "#ffffff",
        titleColor: "#111827",
        textColor: "#6b7280",
      },
    },
    {
      id: "card_2",
      type: "card",
      span: 1,
      props: {
        title: "Analytics",
        content: "Track opens, clicks, and performance.",
        backgroundColor: "#ffffff",
        titleColor: "#111827",
        textColor: "#6b7280",
      },
    },
    {
      id: "card_3",
      type: "card",
      span: 1,
      props: {
        title: "Automation",
        content: "Build workflows for your audience.",
        backgroundColor: "#ffffff",
        titleColor: "#111827",
        textColor: "#6b7280",
      },
    },
    {
      id: "footer_1",
      type: "footer",
      span: 3,
      props: {
        companyName: "{{ company_name }}",
        footerText: "You received this email because you are subscribed.",
        backgroundColor: "#f9fafb",
        textColor: "#6b7280",
      },
    },
  ],
};
