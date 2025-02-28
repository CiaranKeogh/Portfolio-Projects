import { Section } from '@/components/ui/section';
import Image from 'next/image';

interface FeatureProps {
  title: string;
  description: string;
  icon: React.ReactNode;
}

function Feature({ title, description, icon }: FeatureProps) {
  return (
    <div className="flex flex-col items-center text-center p-6">
      <div className="w-16 h-16 rounded-full bg-deep-blue flex items-center justify-center mb-4">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-olive-drab mb-2">{title}</h3>
      <p className="text-off-white/80">{description}</p>
    </div>
  );
}

export function ValuePropositionSection() {
  return (
    <Section
      title="Improve Your Gameplay"
      description="War Thunder Tactics helps you master the battlefield with these powerful features"
    >
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
        <Feature
          title="Interactive Maps"
          description="Explore high-resolution maps with detailed terrain and strategic points of interest."
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-burnt-orange" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
          }
        />
        
        <Feature
          title="Community Tactics"
          description="Discover and share winning strategies, routes, and power positions with other players."
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-burnt-orange" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          }
        />
        
        <Feature
          title="Vehicle-Specific Advice"
          description="Find tactics tailored to your preferred vehicle class, from light tanks to SPAAs."
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-burnt-orange" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          }
        />
      </div>
      
      <div className="bg-gunmetal rounded-lg overflow-hidden shadow-lg">
        <div className="grid grid-cols-1 md:grid-cols-2">
          <div className="p-8 flex flex-col justify-center">
            <h3 className="text-2xl font-bold text-olive-drab mb-4">Draw Routes & Mark Positions</h3>
            <p className="text-off-white/80 mb-6">
              Our interactive tools let you create detailed tactical plans with custom routes, 
              power positions, and line-of-sight visualizations to share with the community.
            </p>
            <ul className="space-y-2">
              {['Color-coded vehicle routes', 'Strategic position marking', 'Line-of-sight visualization', 'Timestamp-based waypoints'].map((feature, index) => (
                <li key={index} className="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-burnt-orange mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-off-white">{feature}</span>
                </li>
              ))}
            </ul>
          </div>
          
          <div className="relative h-64 md:h-auto">
            <Image
              src="/assets/maps/full-size/Fulda Gap/MapLayout_DOMINATION(FULDA_GAP)_Fulda Gap.jpg"
              alt="Interactive map with tactical overlays"
              fill
              className="object-cover"
            />
            <div className="absolute inset-0 bg-deep-blue/30 flex items-center justify-center">
              <div className="bg-gunmetal/80 p-4 rounded-lg">
                <span className="text-off-white font-medium">Interactive Map Preview</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Section>
  );
} 