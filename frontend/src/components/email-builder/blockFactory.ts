import {
  EmailBlock,
  EmailBlockType,
} from "./types";

import { heroDefaults } from "./blocks/hero/defaults";
import { textDefaults } from "./blocks/text/defaults";
import { cardDefaults } from "./blocks/card/defaults";
import { productDefaults } from "./blocks/product/defaults";
import { couponDefaults } from "./blocks/coupon/defaults";
import { buttonDefaults } from "./blocks/button/defaults";
import { imageDefaults } from "./blocks/image/defaults";
import { socialDefaults } from "./blocks/social/defaults";
import { dividerDefaults } from "./blocks/divider/defaults";
import { spacerDefaults } from "./blocks/spacer/defaults";
import { footerDefaults } from "./blocks/footer/defaults";

export function createBlock(
  type: EmailBlockType,
): EmailBlock {
  const id = `${type}_${Date.now()}`;

  switch (type) {
    case "hero":
      return {
        id,
        type,
        span: 3,
        props: heroDefaults,
      };

    case "text":
      return {
        id,
        type,
        span: 3,
        props: textDefaults,
      };

    case "card":
      return {
        id,
        type,
        span: 1,
        props: cardDefaults,
      };

    case "product":
      return {
        id,
        type,
        span: 1,
        props: productDefaults,
      };

    case "coupon":
      return {
        id,
        type,
        span: 2,
        props: couponDefaults,
      };

    case "button":
      return {
        id,
        type,
        span: 3,
        props: buttonDefaults,
      };

    case "image":
      return {
        id,
        type,
        span: 3,
        props: imageDefaults,
      };

    case "social":
      return {
        id,
        type,
        span: 3,
        props: socialDefaults,
      };

    case "divider":
      return {
        id,
        type,
        span: 3,
        props: dividerDefaults,
      };

    case "spacer":
      return {
        id,
        type,
        span: 3,
        props: spacerDefaults,
      };

    case "footer":
    default:
      return {
        id,
        type: "footer",
        span: 3,
        props: footerDefaults,
      };
  }
}
