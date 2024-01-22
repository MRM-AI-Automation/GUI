// Your React component

import React from 'react'
import axios from 'axios'

const CSVsaver = ({ sensorData }) => {
  const flattenObject = (obj) => {
    const flattened = {}

    const flatten = (nested, prefix = '') => {
      for (const [key, value] of Object.entries(nested)) {
        const newKey = prefix ? `${prefix}_${key}` : key

        if (typeof value === 'object' && value !== null) {
          flatten(value, newKey)
        } else {
          flattened[newKey] = value
        }
      }
    }

    flatten(obj)
    return flattened
  }

  const handleSaveCsv = async () => {
    try {
      const flattenedData = flattenObject(sensorData)
      const csvLine = Object.values(flattenedData).join(',')

      await axios.post('/api/save-data', { data: csvLine })
      console.log('Data saved successfully')
    } catch (error) {
      console.error('Error saving data:', error)
    }
  }

  return (
    <div>
      <button onClick={handleSaveCsv}>Save Sensor Data to CSV</button>
    </div>
  )
}

export default CSVsaver
