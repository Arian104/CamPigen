"use client";

import { EmailBlock, EmailBlockType } from "./types";

import { renderHero, HeroProperties, heroHtml } from "./blocks/hero";
import { renderText, TextProperties, textHtml } from "./blocks/text";
import { renderCard, CardProperties, cardHtml } from "./blocks/card";
import { renderProduct, ProductProperties, productHtml } from "./blocks/product";
import { renderCoupon, CouponProperties, couponHtml } from "./blocks/coupon";
import { renderButton, ButtonProperties, buttonHtml } from "./blocks/button";
import { renderImage, ImageProperties, imageHtml } from "./blocks/image";
import { renderSocial, SocialProperties, socialHtml } from "./blocks/social";
import { renderDivider, DividerProperties, dividerHtml } from "./blocks/divider";
import { renderSpacer, SpacerProperties, spacerHtml } from "./blocks/spacer";
import { renderFooter, FooterProperties, footerHtml } from "./blocks/footer";

export type BlockPropertiesProps = {
  block: EmailBlock;
  set: (key: string, value: string) => void;
};

export type BlockConfig = {
  label: string;
  render: (block: EmailBlock) => React.ReactNode;
  html: (block: EmailBlock) => string;
  Properties: (props: BlockPropertiesProps) => React.ReactNode;
};

export const BLOCK_REGISTRY: Record<EmailBlockType, BlockConfig> = {
  hero: {
    label: "Hero",
    render: renderHero,
    html: heroHtml,
    Properties: HeroProperties,
  },
  text: {
    label: "Text",
    render: renderText,
    html: textHtml,
    Properties: TextProperties,
  },
  card: {
    label: "Card",
    render: renderCard,
    html: cardHtml,
    Properties: CardProperties,
  },
  product: {
    label: "Product",
    render: renderProduct,
    html: productHtml,
    Properties: ProductProperties,
  },
  coupon: {
    label: "Coupon",
    render: renderCoupon,
    html: couponHtml,
    Properties: CouponProperties,
  },
  button: {
    label: "Button",
    render: renderButton,
    html: buttonHtml,
    Properties: ButtonProperties,
  },
  image: {
    label: "Image",
    render: renderImage,
    html: imageHtml,
    Properties: ImageProperties,
  },
  social: {
    label: "Social",
    render: renderSocial,
    html: socialHtml,
    Properties: SocialProperties,
  },
  divider: {
    label: "Divider",
    render: renderDivider,
    html: dividerHtml,
    Properties: DividerProperties,
  },
  spacer: {
    label: "Spacer",
    render: renderSpacer,
    html: spacerHtml,
    Properties: SpacerProperties,
  },
  footer: {
    label: "Footer",
    render: renderFooter,
    html: footerHtml,
    Properties: FooterProperties,
  },
};
