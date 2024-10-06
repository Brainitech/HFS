import { useState, useCallback, useRef } from "react"
import Webcam from "react-webcam"
import "../app/globals.css"
import Image from "next/image"

export default function UploadImage() {
  const [selectedFile, setSelectedFile] = useState(null) // Stores selected image file
  const [prediction, setPrediction] = useState("") // Stores the prediction result
  const [isLoading, setIsLoading] = useState(false) // Loading state for feedback
  const [previewImage, setPreviewImage] = useState(null) // Preview for uploaded image
  const [isWebcam, setIsWebcam] = useState(false) // Toggle webcam mode
  const webcamRef = useRef(null) // Ref to access webcam

  // Handle file selection from input
  const handleFileChange = (event) => {
    const file = event.target.files[0]
    if (file) {
      setSelectedFile(file)
      // Generate preview URL
      setPreviewImage(URL.createObjectURL(file))
    }
  }

  // Capture an image from the webcam
  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot()
    if (imageSrc) {
      setPreviewImage(imageSrc)
      fetch(imageSrc)
        .then((res) => res.blob())
        .then((blob) => {
          setSelectedFile(blob)
        })
    }
  }, [webcamRef])

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

  // Hook to select an image based on the prediction result
  const getImageForPrediction = (prediction) => {
    switch (prediction) {
      case "Recyclable":
        return "/1.png"
      case "Organic":
        return "/2.png"
      case "Non_Recyclable":
        return "/3.png"
      default:
        return null
    }
  }

  // Update the image source based on the prediction
  const predictedImage = getImageForPrediction(prediction)

  return (
    <div className="w-screen h-screen bg-[url('/bg2.jpg')] bg-no-repeat bg-cover backdrop-blur-[5px]">
      <div>
        <h1 className="font-bold text-5xl text-center w-screen bg-green-700 bg-opacity-80 backdrop-blur-sm py-4 text-white">AI-Powered Waste Classifier</h1>
        <form className="flex flex-row justify-center gap-32 items-center mt-24" onSubmit={handleSubmit}>
          <div className="flex flex-col w-[500px] h-[600px] rounded-lg border-2 border-green-700 bg-green-400 bg-opacity-50 backdrop-blur-md items-center py-8">
            <label htmlFor="file-upload" className="bg-green-600 bg-opacity-60 backdrop-blur-sm text-white py-4 px-8 w-max rounded-md font-bold text-xl hover:bg-green-600 transition duration-300">
              Upload File
            </label>
            <input type="file" accept="image/*" onChange={handleFileChange} id="file-upload" className="hidden" />

            <button type="button" className="bg-green-600 bg-opacity-60 backdrop-blur-sm text-white py-2 px-4 rounded-md mt-4" onClick={() => setIsWebcam(!isWebcam)}>
              {isWebcam ? "Turn off Webcam" : "Use Webcam"}
            </button>

            {isWebcam && (
              <div className="flex flex-col items-center mt-4">
                <Webcam ref={webcamRef} screenshotFormat="image/jpeg" />
                <button type="button" onClick={capture} className="bg-green-600 bg-opacity-60 backdrop-blur-sm text-white py-2 px-4 rounded-md mt-4">
                  Capture Image
                </button>
              </div>
            )}

            {previewImage && (
              <div className="flex justify-center text-center flex-col items-center mt-4">
                <h3>Selected Image:</h3>
                <img src={previewImage} alt="Selected" width="400px" className="max-h-[400px]" />
              </div>
            )}
          </div>

          <div className="flex flex-col w-[500px] h-[600px] rounded-lg border-2 border-green-700 bg-green-400 bg-opacity-50 backdrop-blur-md items-center py-8">
            <button type="submit" className="bg-green-600 bg-opacity-60 backdrop-blur-sm text-white py-4 px-8 w-max rounded-md font-bold text-xl hover:bg-green-600 transition duration-300">
              Upload & Predict
            </button>
            {isLoading ? (
              <div className="flex justify-center">Loading...</div>
            ) : (
              prediction && (
                <div className="flex flex-col justify-center text-xl font-bold items-center mt-4">
                  <h3>Predicted Class:</h3>
                  <h3 className="font-normal text-md">{prediction}</h3>
                  <Image src={predictedImage} width={300} height={250} alt="RCL" className="mt-4 text-center" />
                </div>
              )
            )}
          </div>
        </form>
      </div>
    </div>
  )
}
