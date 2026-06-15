"use client";

import { EmailBlockType } from "./types";
import styles from "./EmailBuilder.module.css";

type Props = {
  onAddBlock: (type: EmailBlockType) => void;
};

const BLOCKS: { type: EmailBlockType; label: string; description: string }[] = [
  { type: "hero", label: "Hero", description: "Full-width headline" },
  { type: "text", label: "Text", description: "Paragraph content" },
  { type: "card", label: "Card", description: "Small feature block" },
  { type: "product", label: "Product", description: "Product/service card" },
  { type: "coupon", label: "Coupon", description: "Discount offer" },
  { type: "button", label: "Button", description: "CTA button" },
  { type: "image", label: "Image", description: "Banner or visual" },
  { type: "social", label: "Social", description: "Social links" },
  { type: "divider", label: "Divider", description: "Separator" },
  { type: "spacer", label: "Spacer", description: "Vertical spacing" },
  { type: "footer", label: "Footer", description: "Email footer" },
];

export function BlockSidebar({ onAddBlock }: Props) {
  return (
    <aside className={`${styles.sidebar} builderSidebar`}>
      <h3>Blocks</h3>
      <p className="muted">Add sections to the 3-column email canvas.</p>

      <div className={`${styles.blockList} builderBlockList`}>
        {BLOCKS.map((block) => (
          <button
            key={block.type}
            type="button"
            className={`${styles.blockButton} builderBlockButton`}
            onClick={() => onAddBlock(block.type)}
          >
            <strong>{block.label}</strong>
            <span>{block.description}</span>
          </button>
        ))}
      </div>
    </aside>
  );
}
