"use client";

import { uploadPDF } from "@/lib/api";

export default function UploadPDF() {

  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>
  ) {

    const file =
      event.target.files?.[0];

    if (!file) return;

    try {

      const result =
        await uploadPDF(file);

      alert(
        `${result.file} uploaded successfully`
      );

    } catch (error) {

      console.error(error);

      alert(
        "Upload failed"
      );

    }
  }

  return (

    <input
      type="file"
      accept=".pdf"
      onChange={handleUpload}
      className="hidden"
      id="pdf-upload"
    />

  );
}