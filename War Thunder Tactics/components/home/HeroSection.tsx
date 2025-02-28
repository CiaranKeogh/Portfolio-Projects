import Link from 'next/link';

export function HeroSection() {
  return (
    <section className="relative flex items-center justify-center py-24 overflow-hidden bg-gunmetal">
      {/* Background with solid color instead of image */}
      <div className="absolute inset-0 bg-deep-blue/20 z-0">
        <div className="absolute inset-0 bg-gradient-to-b from-gunmetal/70 to-gunmetal"></div>
      </div>
      
      <div className="container mx-auto px-4 z-10 text-center">
        <h1 className="text-5xl md:text-6xl font-bold text-off-white mb-6">
          War Thunder Tactics
        </h1>
        <p className="text-xl md:text-2xl text-off-white/90 mb-8 max-w-3xl mx-auto">
          Master the Battlefield with Strategic Map Knowledge
        </p>
        
        <div className="flex flex-wrap justify-center gap-4 mb-10">
          <div className="bg-deep-blue/80 backdrop-blur-sm py-2 px-4 rounded-full text-off-white">
            <span className="font-medium">Interactive Maps</span>
          </div>
          <div className="bg-olive-drab/80 backdrop-blur-sm py-2 px-4 rounded-full text-off-white">
            <span className="font-medium">Strategic Routes</span>
          </div>
          <div className="bg-burnt-orange/80 backdrop-blur-sm py-2 px-4 rounded-full text-off-white">
            <span className="font-medium">Power Positions</span>
          </div>
        </div>
        
        <Link href="/maps">
          <button className="bg-burnt-orange hover:bg-burnt-orange/90 text-off-white font-bold py-3 px-8 rounded-lg transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Explore Maps
          </button>
        </Link>
      </div>
    </section>
  );
} 