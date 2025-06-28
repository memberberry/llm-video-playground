export interface Video {
  id: number;
  display_name?: string;
  video_uri?: string;
  thumbnail?: string; // Base64 encoded
  gemini_name: string;
  mime_type: string;
  size_bytes: number;
  upload_status: string;
  created_at: string;
  is_deleted: boolean;
  path?: string;
}
