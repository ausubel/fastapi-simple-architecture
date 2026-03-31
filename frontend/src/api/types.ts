export interface PostModel {
  id: number;
  title: string;
  content: string;
  userId: number;
  created_at: string;
  updated_at: string;
}

export interface CreatePostDto {
  title: string;
  content: string;
  user_id: number;
}

export interface LoginDto {
  email: string;
  password: string;
}

export interface TokenDto {
  access_token: string;
  token_type: string;
}

export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
  code?: string;
}
