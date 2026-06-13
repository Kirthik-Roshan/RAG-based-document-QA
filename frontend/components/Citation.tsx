interface CitationProps {

  file: string;

  page:
    | number
    | string;
}

export default function Citation({

  file,
  page,

}: CitationProps) {

  return (

    <div
      className="citation"
    >
      📄 {file}
      {" "}
      (Page {page})
    </div>

  );
}