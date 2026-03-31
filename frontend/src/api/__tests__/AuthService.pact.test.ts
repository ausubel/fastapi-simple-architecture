import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { AuthService } from '../AuthService';
import { describe, it, expect } from 'vitest';
import * as path from 'path';
import type { LoginDto } from '../types';

const { string } = MatchersV3;

const provider = new PactV3({
    consumer: 'FrontendConsumer',
    provider: 'BackendProvider',
    dir: path.resolve(process.cwd(), '../pacts'),
});

describe('AuthService Pact - Login', () => {
    it('returns a token on successful login', async () => {
        const credentials: LoginDto = {
            email: 'test@example.com',
            password: 'password123',
        };

        provider.addInteraction({
            states: [{ description: 'user exists with credentials' }],
            uponReceiving: 'a login request',
            withRequest: {
                method: 'POST',
                path: '/auth/login/',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: credentials,
            },
            willRespondWith: {
                status: 200,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: {
                    success: true,
                    data: {
                        access_token: string('mock.jwt.token'),
                        token_type: string('bearer'),
                    },
                    message: string('Login successful'),
                },
            },
        });

        await provider.executeTest(async (mockServer) => {
            const authService = new AuthService(mockServer.url);
            const response = await authService.login(credentials);
            expect(response.success).toBe(true);
            expect(response.data?.access_token).toBeDefined();
            expect(response.data?.token_type).toBe('bearer');
        });
    });
});
