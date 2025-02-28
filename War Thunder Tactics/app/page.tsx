import { HeroSection } from '@/components/home/hero-section';
import { FeaturedTacticsSection } from '@/components/home/featured-tactics-section';
import { PopularMapsSection } from '@/components/home/popular-maps-section';
import { ValuePropositionSection } from '@/components/home/value-proposition-section';
import { CommunityHighlightSection } from '@/components/home/community-highlight-section';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-24 bg-gunmetal">
      <h1 className="text-4xl font-bold text-off-white mb-6">
        War Thunder Tactics
      </h1>
      <p className="text-xl text-off-white mb-8">
        A community-driven website for War Thunder tactics and strategies
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-deep-blue p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-semibold text-off-white mb-4">Map Guides</h2>
          <p className="text-off-white">Detailed guides for every map in the game.</p>
        </div>
        <div className="bg-olive-drab p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-semibold text-off-white mb-4">Vehicle Tactics</h2>
          <p className="text-off-white">Learn the best ways to use different vehicles.</p>
        </div>
        <div className="bg-burnt-orange p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-semibold text-off-white mb-4">Community Tips</h2>
          <p className="text-off-white">Tips and tricks from experienced players.</p>
        </div>
      </div>
    </main>
  );
} 