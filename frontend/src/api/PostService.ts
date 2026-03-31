import axios from 'axios';
import type { PostModel, ApiResponse, CreatePostDto } from './types';

export class PostService {
  private url: string;

  constructor(url: string) {
    this.url = url;
  }

  async getPosts(): Promise<ApiResponse<PostModel[]>> {
    const response = await axios.get<ApiResponse<PostModel[]>>(`${this.url}/posts/`);
    return response.data;
  }

  async getPostById(id: number): Promise<ApiResponse<PostModel>> {
    const response = await axios.get<ApiResponse<PostModel>>(`${this.url}/posts/${id}/`);
    return response.data;
  }

  async createPost(post: CreatePostDto): Promise<ApiResponse> {
    const response = await axios.post<ApiResponse>(`${this.url}/posts/`, post);
    return response.data;
  }
}
