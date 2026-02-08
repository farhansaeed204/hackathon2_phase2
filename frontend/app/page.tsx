'use client';

import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl">
        <div className="p-8">
          <div className="flex items-center justify-center">
            <h1 className="text-3xl font-bold text-gray-800">HK2 Phase II</h1>
          </div>
          <p className="mt-4 text-center text-gray-600">
            Welcome to the Hackathon Phase II Task Management Application
          </p>
          <div className="mt-8 flex justify-center">
            <Link href="/tasks" className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded inline-flex items-center">
              View Tasks
            </Link>
          </div>
          <div className="mt-4 flex justify-center">
            <Link href="/login" className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
              Login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}