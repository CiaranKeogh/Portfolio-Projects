import { MapCard } from '@/components/maps/map-card';
import { Section } from '@/components/ui/section';
import { getTopMaps } from '@/lib/map-utils';

export function PopularMapsSection() {
  const maps = getTopMaps(6);
  
  return (
    <Section
      title="Popular Maps"
      description="Explore the most played battlefields in War Thunder"
      viewAllLink="/maps"
      viewAllText="View All Maps"
      className="bg-gunmetal/30"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {maps.map((map) => (
          <MapCard key={map.id} map={map} />
        ))}
      </div>
    </Section>
  );
} 