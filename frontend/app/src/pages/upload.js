import { useState } from "react"

export default function UploadImage() {
  const [selectedFile, setSelectedFile] = useState(null) // Stores selected image file
  const [prediction, setPrediction] = useState("") // Stores the prediction result
  const [isLoading, setIsLoading] = useState(false) // Loading state for feedback
  const [previewImage, setPreviewImage] = useState(null) // Preview for uploaded image

  // Handle file selection from input
  const handleFileChange = (event) => {
    const file = event.target.files[0]
    if (file) {
      setSelectedFile(file)
      // Generate preview URL
      setPreviewImage(URL.createObjectURL(file))
    }
  }

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!selectedFile) {
      alert("Please select an image first.")
      return
    }

    // Create FormData to send the image file in the POST request
    const formData = new FormData()
    formData.append("file", selectedFile)

    try {
      setIsLoading(true) // Show loading state
      const response = await fetch("http://localhost:8000/predict/", {
        method: "POST",
        body: formData,
      })

      const result = await response.json()
      setPrediction(result.predicted_class) // Set the prediction result
      setIsLoading(false) // Stop loading state
    } catch (error) {
      console.error("Error:", error)
      setIsLoading(false)
    }
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Garbage Classification</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button type="submit" style={{ marginTop: "10px" }}>
          Upload & Predict
        </button>
      </form>

      {/* Show image preview */}
      {previewImage && (
        <div style={{ marginTop: "20px" }}>
          <h3>Selected Image:</h3>
          <img src={previewImage} alt="Selected" width="300px" />
        </div>
      )}

      {/* Show loading spinner or prediction result */}
      {isLoading ? (
        <div style={{ marginTop: "20px" }}>Loading...</div>
      ) : (
        prediction && (
          <div style={{ marginTop: "20px" }}>
            <h3>Predicted Class: {prediction}</h3>
          </div>
        )
      )}
    </div>
  )
}
