import { EmailBlock, EmailBuilderSchema } from "./types";
import { BLOCK_REGISTRY } from "./blockRegistry";

function blockHtml(block: EmailBlock) {
  const config = BLOCK_REGISTRY[block.type];
  return config.html(block);
}

function packRows(blocks: EmailBlock[]) {
  const rows: EmailBlock[][] = [];
  let currentRow: EmailBlock[] = [];
  let used = 0;

  blocks.forEach((block) => {
    const span = Math.min(Math.max(block.span || 3, 1), 3);

    if (used + span > 3) {
      rows.push(currentRow);
      currentRow = [];
      used = 0;
    }

    currentRow.push({
      ...block,
      span: span as 1 | 2 | 3,
    });

    used += span;

    if (used === 3) {
      rows.push(currentRow);
      currentRow = [];
      used = 0;
    }
  });

  if (currentRow.length > 0) {
    rows.push(currentRow);
  }

  return rows;
}

export function compileEmailHtml(schema: EmailBuilderSchema) {
  const rows = packRows(schema.blocks);

  const rowsHtml = rows
    .map((row) => {
      const cells = row
        .map((block) => {
          const colspan = block.span;

          return `
            <td colspan="${colspan}" width="${(colspan / 3) * 100}%" valign="top" style="padding:10px;">
              ${blockHtml(block)}
            </td>
          `;
        })
        .join("");

      return `<tr>${cells}</tr>`;
    })
    .join("");

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body style="margin:0; padding:0; background:#eef2f7; font-family:Arial, Helvetica, sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#eef2f7; padding:40px 0;">
    <tr>
      <td align="center">
        <table width="650" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:22px; overflow:hidden; padding:18px;">
          ${rowsHtml}
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
  `;
}
