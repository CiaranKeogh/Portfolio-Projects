import { HeroSection } from '@/components/home/HeroSection';
import { MapCarousel } from '@/components/home/MapCarousel';
import { PowerPositionsSection } from '@/components/home/PowerPositionsSection';
import { StrategicRoutesSection } from '@/components/home/StrategicRoutesSection';
import { CommunityStatsSection } from '@/components/home/CommunityStatsSection';

export default function Home() {
  return (
    <main className="min-h-screen bg-gunmetal/90">
      <HeroSection />
      <MapCarousel />
      <PowerPositionsSection />
      <StrategicRoutesSection />
      <CommunityStatsSection />
    </main>
  );
} 