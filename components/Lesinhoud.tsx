import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

/**
 * Toont de theorie van een les.
 *
 * react-markdown laat standaard GEEN rauwe HTML door. Dat houden we zo: de
 * tekst komt uit een formulier, en een les met een stukje script erin zou op
 * het scherm van elke leerling uitgevoerd worden.
 */
export default function Lesinhoud({ markdown }: { markdown: string }) {
  return (
    <div className="lesinhoud">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown>
    </div>
  );
}
