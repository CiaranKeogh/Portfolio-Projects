import Link from 'next/link';

export function Footer() {
  return (
    <footer className="bg-gunmetal mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold text-olive-drab mb-4">War Thunder Tactics</h3>
            <p className="text-off-white opacity-80">Community-driven tactics and strategies for War Thunder players.</p>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold text-burnt-orange mb-3">Navigation</h4>
            <ul className="space-y-2">
              <li><Link href="/" className="text-off-white hover:text-burnt-orange transition">Home</Link></li>
              <li><Link href="/maps" className="text-off-white hover:text-burnt-orange transition">Maps</Link></li>
              <li><Link href="/tactics" className="text-off-white hover:text-burnt-orange transition">Tactics</Link></li>
              <li><Link href="/community" className="text-off-white hover:text-burnt-orange transition">Community</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold text-burnt-orange mb-3">Resources</h4>
            <ul className="space-y-2">
              <li><Link href="/faq" className="text-off-white hover:text-burnt-orange transition">FAQ</Link></li>
              <li><Link href="/guides" className="text-off-white hover:text-burnt-orange transition">Guides</Link></li>
              <li><Link href="/contribute" className="text-off-white hover:text-burnt-orange transition">Contribute</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold text-burnt-orange mb-3">Legal</h4>
            <ul className="space-y-2">
              <li><Link href="/terms" className="text-off-white hover:text-burnt-orange transition">Terms of Service</Link></li>
              <li><Link href="/privacy" className="text-off-white hover:text-burnt-orange transition">Privacy Policy</Link></li>
              <li><Link href="/disclaimer" className="text-off-white hover:text-burnt-orange transition">Disclaimer</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-6 text-center text-off-white opacity-70">
          <p>War Thunder Tactics is a fan-made site and is not affiliated with Gaijin Entertainment.</p>
          <p className="mt-2">&copy; {new Date().getFullYear()} War Thunder Tactics. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
} 