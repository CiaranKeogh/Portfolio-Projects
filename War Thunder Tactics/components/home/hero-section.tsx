import Link from 'next/link';
import Image from 'next/image';

export function HeroSection() {
  return (
    <section className="relative bg-gunmetal overflow-hidden">
      {/* Background image with overlay */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-r from-gunmetal via-gunmetal/90 to-gunmetal/70 z-10" />
        <Image
          src="/assets/maps/full-size/Berlin/MapLayout_DOMINATION(BERLIN)_Berlin.jpg"
          alt="War Thunder Map"
          fill
          className="object-cover opacity-40"
          priority
        />
      </div>
      
      <div className="container mx-auto px-4 py-16 md:py-24 relative z-10">
        <div className="max-w-3xl">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-off-white mb-4">
            Master the Battlefield with Community Tactics
          </h1>
          
          <p className="text-xl text-off-white/90 mb-8 max-w-2xl">
            Discover optimal routes, power positions, and winning strategies shared by the War Thunder community.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4">
            <Link 
              href="/maps" 
              className="px-6 py-3 bg-burnt-orange text-off-white font-medium rounded-md hover:bg-burnt-orange/90 transition flex items-center justify-center"
            >
              Explore Maps
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                className="h-5 w-5 ml-2" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
            
            <Link 
              href="/tactics" 
              className="px-6 py-3 bg-deep-blue text-off-white font-medium rounded-md hover:bg-deep-blue/90 transition flex items-center justify-center"
            >
              View Popular Tactics
            </Link>
          </div>
          
          <div className="mt-12 flex items-center">
            <div className="flex -space-x-2">
              {/* User avatars - would be dynamic in a real app */}
              {[1, 2, 3, 4].map((i) => (
                <div 
                  key={i} 
                  className="w-8 h-8 rounded-full bg-olive-drab flex items-center justify-center border-2 border-gunmetal"
                >
                  <span className="text-off-white text-xs font-bold">
                    {String.fromCharCode(64 + i)}
                  </span>
                </div>
              ))}
            </div>
            <span className="ml-4 text-off-white/80 text-sm">
              Join the community of War Thunder tacticians
            </span>
          </div>
        </div>
      </div>
    </section>
  );
} 