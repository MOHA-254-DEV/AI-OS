import React from 'react'
import productData from './mock_data.json'

export default function Storefront() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-6 bg-gray-50">
      {productData.map(product => (
        <div key={product.id} className="rounded-2xl shadow-md p-4 bg-white">
          <h2 className="text-xl font-semibold">{product.name}</h2>
          <p className="text-gray-500">{product.category}</p>
          <p className="text-green-600 text-lg font-bold">${product.price || product.base_price}</p>
          <button className="mt-2 px-4 py-1 bg-blue-600 text-white rounded-full hover:bg-blue-700">
            Buy Now
          </button>
        </div>
      ))}
    </div>
  )
}
