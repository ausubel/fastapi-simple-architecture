import { useEffect, useState } from 'react';
import { PostService } from '../api/PostService';
import type { PostModel } from '../api/types';

interface PostListProps {
  onPostClick: (post: PostModel) => void;
}

const API_URL = 'http://localhost:8000';

export function PostList({ onPostClick }: PostListProps) {
  const [posts, setPosts] = useState<PostModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const service = new PostService(API_URL);
        const response = await service.getPosts();
        if (response.success && response.data) {
          setPosts(response.data);
        } else {
          setError(response.message || 'Failed to load posts');
        }
      } catch (err) {
        setError('Error connecting to server');
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (loading) return <div className="loading">Loading posts...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="post-list">
      <h2>All Posts</h2>
      {posts.length === 0 ? (
        <p>No posts available</p>
      ) : (
        <div className="posts-grid">
          {posts.map((post) => (
            <div
              key={post.id}
              className="post-card"
              onClick={() => onPostClick(post)}
            >
              <h3>{post.title}</h3>
              <p className="post-content">{post.content.substring(0, 100)}...</p>
              <span className="post-date">
                {new Date(post.created_at).toLocaleDateString()}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
