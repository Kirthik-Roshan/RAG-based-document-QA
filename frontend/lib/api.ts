const BASE_URL = "http://127.0.0.1:8000";

export async function uploadPDF(
  file: File
) {
  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  const response = await fetch(
    `${BASE_URL}/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error(
      "Upload failed"
    );
  }

  return response.json();
}

export async function askQuestion(
  question: string
) {
  const response = await fetch(
    `${BASE_URL}/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",
      },

      body: JSON.stringify({
        question,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      "Chat request failed"
    );
  }

  return response.json();
}