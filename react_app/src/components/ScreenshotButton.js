import React from 'react'
import html2canvas from 'html2canvas'

const ScreenshotButton = () => {
  const handleScreenshot = () => {
    const targetElement = document.documentElement

    html2canvas(targetElement, { scale: 2 }).then((canvas) => {
      // Convert the canvas to a data URL
      const screenshotDataUrl = canvas.toDataURL()

      // Create a link element and trigger a download
      const link = document.createElement('a')
      link.href = screenshotDataUrl
      link.download = 'screenshot.png'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    })
  }

  return (
    <div>
      <button id='four' onClick={handleScreenshot}>
        Take Screenshot
      </button>
    </div>
  )
}

export default ScreenshotButton
