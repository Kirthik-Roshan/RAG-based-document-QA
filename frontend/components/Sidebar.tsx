"use client";

import UploadPDF from "./UploadPDF";

export default function Sidebar() {

  return (

    <aside className="sidebar">

      <div>

        <h1 className="logo">
          🦇 BATCAVE AI
        </h1>

        <label
          htmlFor="pdf-upload"
          className="new-chat"
        >
          Upload PDF
        </label>

        <UploadPDF />

      </div>

      <div className="recent">

        <h3>
          DOCUMENTS
        </h3>

        <p>
          Uploaded PDFs appear here
        </p>

      </div>

    </aside>

  );
}