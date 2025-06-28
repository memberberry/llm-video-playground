export interface History {
  hash: string;
  prompt: string;
  model: string;
  output?: string;
  structured_output?: any; // Use 'any' for now, can be more specific later
  created_at: string;
  videos: number[];
}
