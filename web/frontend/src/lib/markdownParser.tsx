/**
 * Simple markdown parser for rendering markdown text in React
 */

interface MarkdownNode {
  type: 'heading2' | 'paragraph' | 'bold' | 'list' | 'ordered_list' | 'text';
  content?: string;
  children?: MarkdownNode[];
}

// Helper function to render inline bold text
function renderInlineBold(text: string): React.ReactNode[] {
  const parts = text.split(/(\*\*[^*]+\*\*)/);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return (
        <strong key={i} className="text-foreground font-semibold">
          {part.replace(/\*\*/g, '')}
        </strong>
      );
    }
    return part;
  });
}

export function parseMarkdown(text: string): MarkdownNode[] {
  const lines = text.split('\n');
  const nodes: MarkdownNode[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Skip empty lines
    if (!line.trim()) {
      i++;
      continue;
    }

    // Heading 2
    if (line.startsWith('## ')) {
      nodes.push({
        type: 'heading2',
        content: line.replace(/^## /, ''),
      });
      i++;
      continue;
    }

    // Unordered list
    if (line.trim().startsWith('- ')) {
      const listItems: string[] = [];
      while (i < lines.length && lines[i].trim().startsWith('- ')) {
        listItems.push(lines[i].replace(/^- /, ''));
        i++;
      }
      nodes.push({
        type: 'list',
        children: listItems.map((item) => ({
          type: 'text' as const,
          content: item,
        })),
      });
      continue;
    }

    // Ordered list
    if (line.match(/^\d+\. /)) {
      const listItems: string[] = [];
      while (i < lines.length && lines[i].match(/^\d+\. /)) {
        listItems.push(lines[i].replace(/^\d+\. /, ''));
        i++;
      }
      nodes.push({
        type: 'ordered_list',
        children: listItems.map((item) => ({
          type: 'text' as const,
          content: item,
        })),
      });
      continue;
    }

    // Regular paragraph
    if (line.trim()) {
      nodes.push({
        type: 'paragraph',
        content: line,
      });
      i++;
      continue;
    }

    i++;
  }

  return nodes;
}

export function renderMarkdownNode(node: MarkdownNode, index: number): React.ReactNode {
  switch (node.type) {
    case 'heading2':
      return (
        <h2 key={index} className="font-serif text-xl font-semibold mt-8 mb-4 text-foreground">
          {node.content}
        </h2>
      );

    case 'paragraph':
      // Parse inline bold text
      return (
        <p key={index} className="text-foreground/90 leading-relaxed mb-4">
          {renderInlineBold(node.content!)}
        </p>
      );

    case 'list':
      return (
        <ul key={index} className="list-disc list-inside space-y-2 mb-4 ml-2">
          {node.children?.map((child, i) => (
            <li key={i} className="text-foreground/90">
              {renderInlineBold(child.content!)}
            </li>
          ))}
        </ul>
      );

    case 'ordered_list':
      return (
        <ol key={index} className="list-decimal list-inside space-y-2 mb-4 ml-2">
          {node.children?.map((child, i) => (
            <li key={i} className="text-foreground/90">
              {renderInlineBold(child.content!)}
            </li>
          ))}
        </ol>
      );

    default:
      return null;
  }
}

export function renderMarkdown(markdown: string): React.ReactNode[] {
  const nodes = parseMarkdown(markdown);
  return nodes.map((node, index) => renderMarkdownNode(node, index));
}
