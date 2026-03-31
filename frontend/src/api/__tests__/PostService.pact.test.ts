import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { PostService } from '../PostService';
import { describe, it, expect } from 'vitest';
import * as path from 'path';

const { eachLike, integer, string, boolean } = MatchersV3;

const provider = new PactV3({
    consumer: 'FrontendConsumer',
    provider: 'BackendProvider',
    dir: path.resolve(process.cwd(), '../pacts'),
});

describe('PostService Pact', () => {
    it('returns all posts', async () => {
        provider.addInteraction({
            states: [{ description: 'posts exist' }],
            uponReceiving: 'a request for all posts',
            withRequest: {
                method: 'GET',
                path: '/posts/',
            },
            willRespondWith: {
                status: 200,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: {
                    success: boolean(true),
                    data: eachLike({
                        id: integer(1),
                        title: string('Pact Title'),
                        content: string('Pact Content'),
                        userId: integer(2),
                        created_at: string('2024-01-01T00:00:00Z'),
                        updated_at: string('2024-01-01T00:00:00Z'),
                    }),
                    message: string('Posts retrieved successfully'),
                },
            },
        });

        await provider.executeTest(async (mockServer) => {
            const postService = new PostService(mockServer.url);
            const response = await postService.getPosts();
            expect(response.success).toBe(true);
            expect(response.data!.length).toBeGreaterThan(0);
        });
    });
});
