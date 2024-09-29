"use client"; // Ensure this is a Client Component in Next.js

import React, { useState } from "react";

export default function HeroHome() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false); // Track the upload status

  // Handle file selection and automatic upload
  const handleFileSelect = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setSelectedFile(file);

      // Automatically start the upload process after the file is selected
      await handleFileUpload(file);
    }
  };

  // Handle the actual file upload process
  const handleFileUpload = async (file: File) => {
    setUploading(true); // Set uploading state to true

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        alert("File uploaded successfully");
        setSelectedFile(null); // Clear the selected file after successful upload
      } else {
        alert("File upload failed");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("An error occurred while uploading the file.");
    } finally {
      setUploading(false); // Reset uploading state
    }
  };

  // Placeholder function for verifying credentials
  const handleVerifyCredentials = () => {
    alert("Verify Credentials functionality goes here.");
  };

  return (
    <section>
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="py-12 md:py-20">
          {/* Header */}
          <div className="pb-12 text-center md:pb-20">
            <h1 className="text-4xl font-semibold">
              Blockchain-Powered Credential Solutions for Secure Verification
            </h1>
            <div className="mx-auto max-w-3xl">
              <p className="mb-8 text-xl">
                Our platform enables institutions and employers to securely
                verify academic and professional credentials, ensuring
                authenticity and reducing fraud.
              </p>

              {/* Buttons Section */}
              <div className="mx-auto max-w-xs sm:flex sm:max-w-none sm:justify-center">
                <div className="flex flex-col sm:mr-4">
                  {/* Add Credentials Button */}
                  <input
                    type="file"
                    onChange={handleFileSelect}
                    style={{ display: "none" }}
                    id="file-upload"
                  />
                  <button
                    className="btn mb-4 w-full bg-indigo-600 text-white"
                    onClick={() =>
                      document.getElementById("file-upload")?.click()
                    }
                    disabled={uploading} // Disable the button while uploading
                  >
                    {uploading ? "Uploading..." : "Add Credentials"}
                  </button>
                </div>

                <div className="flex flex-col sm:ml-4">
                  {/* Verify Credentials Button */}
                  <button
                    className="btn mb-4 w-full bg-gray-800 text-white"
                    onClick={handleVerifyCredentials}
                  >
                    Verify Credentials
                  </button>
                </div>
              </div>

              {/* Display selected file name (optional) */}
              {selectedFile && !uploading && (
                <p className="text-center text-gray-500 mt-4">
                  Selected File: {selectedFile.name}
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
