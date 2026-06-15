"use client";

import { useEffect, useMemo, useState } from "react";

import { BlockSidebar } from "./BlockSidebar";
import { BuilderCanvas } from "./BuilderCanvas";
import { PropertyPanel } from "./PropertyPanel";

import { compileEmailHtml } from "./compileEmailHtml";
import { createBlock } from "./blockFactory";

import {
  DEFAULT_SCHEMA,
  EmailBlock,
  EmailBlockType,
  EmailBuilderSchema,
} from "./types";
import styles from "./EmailBuilder.module.css";

type Props = {
  initialSchema?: EmailBuilderSchema | null;
  onChange: (
    schema: EmailBuilderSchema,
    html: string,
  ) => void;
};

function cloneSchema(
  schema: EmailBuilderSchema,
): EmailBuilderSchema {
  return JSON.parse(JSON.stringify(schema));
}

function builderSafeKey(
  schema?: EmailBuilderSchema | null,
) {
  if (!schema) return "empty";

  return JSON.stringify(
    schema.blocks.map((block) => ({
      id: block.id,
      type: block.type,
      span: block.span,
    })),
  );
}

function normalizeSchema(
  schema?: EmailBuilderSchema | null,
): EmailBuilderSchema {
  if (
    !schema ||
    !Array.isArray(schema.blocks)
  ) {
    return cloneSchema(DEFAULT_SCHEMA);
  }

  return {
    columns: 3,

    blocks: schema.blocks.map((block) => ({
      ...block,

      span: block.span ?? 3,

      props: block.props ?? {},
    })),
  };
}

export function EmailBuilder({
  initialSchema,
  onChange,
}: Props) {
  const [schema, setSchema] =
    useState<EmailBuilderSchema>(() =>
      normalizeSchema(initialSchema),
    );

  const [selectedBlockId, setSelectedBlockId] =
    useState<string | null>(
      schema.blocks[0]?.id ?? null,
    );

  const selectedBlock = useMemo(
    () =>
      schema.blocks.find(
        (block) =>
          block.id === selectedBlockId,
      ) ?? null,

    [schema.blocks, selectedBlockId],
  );

  /*
    Prevent infinite rerender loop
    when parent passes new object refs
  */

  useEffect(() => {
    if (!initialSchema) return;

    const normalized =
      normalizeSchema(initialSchema);

    const current = JSON.stringify(
      schema.blocks,
    );

    const incoming = JSON.stringify(
      normalized.blocks,
    );

    if (current !== incoming) {
      setSchema(normalized);

      setSelectedBlockId(
        normalized.blocks[0]?.id ??
          null,
      );
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [builderSafeKey(initialSchema)]);

  /*
    Generate HTML whenever schema changes
  */

  useEffect(() => {
    const html =
      compileEmailHtml(schema);

    onChange(schema, html);

  }, [schema, onChange]);

  function updateBlocks(
    blocks: EmailBlock[],
  ) {
    setSchema({
      columns: 3,
      blocks,
    });
  }

  function addBlock(
    type: EmailBlockType,
  ) {
    const block = createBlock(type);

    updateBlocks([
      ...schema.blocks,
      block,
    ]);

    setSelectedBlockId(block.id);
  }

  function updateBlock(
    updatedBlock: EmailBlock,
  ) {
    updateBlocks(
      schema.blocks.map((block) =>
        block.id === updatedBlock.id
          ? updatedBlock
          : block,
      ),
    );

    setSelectedBlockId(
      updatedBlock.id,
    );
  }

  function deleteBlock(id: string) {
    const nextBlocks =
      schema.blocks.filter(
        (block) =>
          block.id !== id,
      );

    updateBlocks(nextBlocks);

    if (selectedBlockId === id) {
      setSelectedBlockId(
        nextBlocks[0]?.id ??
          null,
      );
    }
  }

  return (
    <div className={`${styles.shell} emailBuilderShell`}>
      <BlockSidebar
        onAddBlock={addBlock}
      />

      <BuilderCanvas
        blocks={schema.blocks}
        selectedBlockId={
          selectedBlockId
        }
        onSelectBlock={
          setSelectedBlockId
        }
        onDeleteBlock={
          deleteBlock
        }
        onReorder={updateBlocks}
      />

      <PropertyPanel
        block={selectedBlock}
        onUpdateBlock={
          updateBlock
        }
      />
    </div>
  );
}
