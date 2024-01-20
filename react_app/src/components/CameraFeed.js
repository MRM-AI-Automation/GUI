import React, { useEffect, useState, useRef } from 'react'
import socketIOClient from 'socket.io-client'

const CameraFeed = () => {
  const videoRef = useRef()
  console.log('Hi')

  useEffect(() => {
    const socket = socketIOClient('http://localhost:5000/camera')

    socket.on('frame', (data) => {
      console.log('Received frame:', data)
      const frame = data.data
      const videoElement = videoRef.current
      videoElement.src = `data:image/jpeg;base64,${frame}`
    })

    return () => {
      socket.disconnect()
    }
  }, [])

  return <video ref={videoRef} autoPlay />
}

export default CameraFeed
