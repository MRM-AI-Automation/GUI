import React from 'react'
import html2canvas from 'html2canvas'
import domtoimage from 'dom-to-image'

const ScreenshotButton = ({ id }) => {
  const handleScreenshot = () => {
    // const targetElement = microscopeRef.current

    domtoimage
      // .toPng(targetElement)
      .then((dataUrl) => {
        const link = document.createElement('a')
        link.href = dataUrl
        link.download = 'microscope_screenshot.png'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      })
      .catch((error) => {
        console.error('Error capturing screenshot:', error)
      })
  }

  return (
    <div>
      <button id={id} onClick={handleScreenshot}>
        Take Screenshot
      </button>
    </div>
  )
}

export default ScreenshotButton
