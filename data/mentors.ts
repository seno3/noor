export interface Mentor {
  id: string;
  name: string;
  title: string;
  bio: string;
  imageUrl: string;
  calendlyUrl: string;
}

export const mentors: Mentor[] = [
  {
    id: 'ahmed',
    name: 'Ahmed Malik',
    title: 'MSA President & CS Senior',
    bio: 'Assalamu Alaikum! I reverted 3 years ago and I remember how overwhelming it was. I\'m here to answer any questions you have—no judgment, ever.',
    imageUrl: 'https://placehold.co/100x100/E2D6FF/3D2C80?text=AM',
    calendlyUrl: 'https://calendly.com/senosanjeev1/30min',
  },
  {
    id: 'fatima',
    name: 'Fatima Al-Sayed',
    title: 'Alima-in-Training & Psych Major',
    bio: 'Salaam! I grew up in a Muslim family but am formally studying our deen. I specialize in spiritual wellness and finding your "why". Happy to just listen.',
    imageUrl: 'https://placehold.co/100x100/FFD6F5/802C7E?text=FA',
    calendlyUrl: 'https://calendly.com/senosanjeev1/30min',
  },
];

