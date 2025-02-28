import Link from 'next/link';
import Image from 'next/image';

export function Header() {
  return (
    <header className="bg-gunmetal shadow-md">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center">
          <Link href="/" className="flex items-center">
            <span className="text-2xl font-bold text-olive-drab">WT Tactics</span>
          </Link>
        </div>
        
        <nav className="hidden md:flex space-x-8">
          <Link href="/maps" className="text-off-white hover:text-burnt-orange transition">
            Maps
          </Link>
          <Link href="/tactics" className="text-off-white hover:text-burnt-orange transition">
            Tactics
          </Link>
          <Link href="/community" className="text-off-white hover:text-burnt-orange transition">
            Community
          </Link>
        </nav>
        
        <div className="flex items-center space-x-4">
          <Link href="/login" className="px-4 py-2 rounded bg-deep-blue text-off-white hover:bg-opacity-90 transition">
            Login
          </Link>
          <Link href="/signup" className="px-4 py-2 rounded bg-burnt-orange text-off-white hover:bg-opacity-90 transition">
            Sign Up
          </Link>
          
          {/* Mobile menu button */}
          <button className="md:hidden text-off-white">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
} 