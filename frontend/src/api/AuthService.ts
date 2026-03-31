import axios from 'axios';
import type { LoginDto, TokenDto, ApiResponse } from './types';

export class AuthService {
  private url: string;

  constructor(url: string) {
    this.url = url;
  }

  async login(credentials: LoginDto): Promise<ApiResponse<TokenDto>> {
    const response = await axios.post<ApiResponse<TokenDto>>(`${this.url}/auth/login/`, credentials);
    return response.data;
  }
}
