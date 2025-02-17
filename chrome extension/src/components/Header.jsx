import React from 'react';
import logo from './logo.png';

const Header = () => {
  return (
    <header className="bg-[#0D1821] text-white shadow-lg">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20"> {/* Increased height */}
          {/* Logo Section */}
          <div className="flex items-center text-2xl">
            Routine Radar
          </div>

          {/* Greeting Section */}
          <div className="flex items-center">
            <p className="text-[#5CC8FF] font-medium text-lg"> {/* Increased text size */}
              Welcome back, <span className="text-white">Karan Brar!</span>
            </p>
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;