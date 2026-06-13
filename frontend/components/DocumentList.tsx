interface DocumentListProps {

  documents: string[];
}

export default function DocumentList({

  documents,

}: DocumentListProps) {

  return (

    <div>

      {documents.map(
        (
          doc,
          index
        ) => (

          <p key={index}>
            📄 {doc}
          </p>

        )
      )}

    </div>

  );
}