import React from 'react'
import { Shield } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white shadow-2xl">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Shield className="w-10 h-10" />
            <div>
              <h1 className="text-3xl font-bold">AVRT™ Firewall</h1>
              <p className="text-sm text-blue-100">
                Advanced Voice Reasoning Technology
              </p>
            </div>
          </div>
          <div className="hidden md:flex flex-col items-end text-sm">
            <p className="font-semibold">SPIEL™ + THT™ Active</p>
            <p className="text-blue-100">Patent: USPTO #19/236,935</p>
          </div>
        </div>

        <div className="mt-4 flex gap-4 text-sm">
          <div className="bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full">
            <span className="font-semibold">SPIEL™:</span> Safety · Personalization · Integrity · Ethics · Logic
          </div>
          <div className="bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full">
            <span className="font-semibold">THT™:</span> Truth · Honesty · Transparency
          </div>
        </div>
      </div>
    </header>
  )
}
