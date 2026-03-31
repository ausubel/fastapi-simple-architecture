import type { PostModel } from '../api/types';

interface PostDetailProps {
  post: PostModel;
  onBack: () => void;
}

export function PostDetail({ post, onBack }: PostDetailProps) {
  return (
    <div className="post-detail">
      <button onClick={onBack} className="back-btn">← Back to Posts</button>
      <article>
        <h2>{post.title}</h2>
        <div className="post-meta">
          <span>By User #{post.userId}</span>
          <span>{new Date(post.created_at).toLocaleString()}</span>
        </div>
        <div className="post-full-content">
          {post.content}
        </div>
        <div className="post-footer">
          <small>Last updated: {new Date(post.updated_at).toLocaleString()}</small>
        </div>
      </article>
    </div>
  );
}
