"use client";

import { CSS } from "@dnd-kit/utilities";
import { useSortable } from "@dnd-kit/sortable";

import { EmailBlock } from "./types";
import { BLOCK_REGISTRY } from "./blockRegistry";
import styles from "./EmailBuilder.module.css";

type Props = {
  block: EmailBlock;
  selected: boolean;
  onSelect: () => void;
  onDelete: () => void;
};

export function SortableEmailBlock({
  block,
  selected,
  onSelect,
  onDelete,
}: Props) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({
    id: block.id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    gridColumn: `span ${block.span}`,
  };

  const config = BLOCK_REGISTRY[block.type];

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={selected ? `${styles.emailBlock} ${styles.selected} sortableEmailBlock selected` : `${styles.emailBlock} sortableEmailBlock`}
      onClick={onSelect}
    >
      <div className={`${styles.blockToolbar} blockToolbar`}>
        <button type="button" className="dragHandle" {...attributes} {...listeners}>
          Drag
        </button>

        <span className="blockSpanBadge">{block.span}/3</span>

        <button
          type="button"
          className="dangerButton smallButton"
          onClick={(event) => {
            event.stopPropagation();
            onDelete();
          }}
        >
          Delete
        </button>
      </div>

      {config.render(block)}
    </div>
  );
}
