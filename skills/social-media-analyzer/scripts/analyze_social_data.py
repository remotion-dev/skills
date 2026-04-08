#!/usr/bin/env python3
"""
Social Media Performance Analyzer
Processes scraped social media data and generates analysis metrics.
Used by the social-media-analyzer skill to produce weekly reports.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from statistics import mean, stdev


def load_json(filepath):
    """Load a JSON file safely."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load {filepath}: {e}")
        return None


def save_json(data, filepath):
    """Save data as JSON."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)


# ─── Instagram Analysis ───────────────────────────────────────────

def analyze_instagram(profile_data, posts_data, prev_profile=None, prev_posts=None):
    """Analyze Instagram performance metrics."""
    if not profile_data or not posts_data:
        return {"status": "no_data", "message": "Instagram data not available"}

    followers = profile_data.get("followersCount", profile_data.get("followers", 0))
    following = profile_data.get("followingCount", profile_data.get("following", 0))
    post_count = profile_data.get("postsCount", profile_data.get("posts", 0))

    # Per-post metrics
    post_metrics = []
    for post in posts_data:
        likes = post.get("likesCount", post.get("likes", 0)) or 0
        comments = post.get("commentsCount", post.get("comments", 0)) or 0
        saves = post.get("savesCount", post.get("saves", 0)) or 0
        shares = post.get("sharesCount", post.get("shares", 0)) or 0

        engagement = likes + comments + saves + shares
        eng_rate = (engagement / followers * 100) if followers > 0 else 0

        post_metrics.append({
            "url": post.get("url", ""),
            "caption": (post.get("caption", "") or "")[:200],
            "type": post.get("type", "unknown"),
            "timestamp": post.get("timestamp", ""),
            "likes": likes,
            "comments": comments,
            "saves": saves,
            "shares": shares,
            "total_engagement": engagement,
            "engagement_rate": round(eng_rate, 2),
            "hashtags": post.get("hashtags", []),
        })

    # Sort by engagement rate
    post_metrics.sort(key=lambda x: x["engagement_rate"], reverse=True)

    avg_eng_rate = mean([p["engagement_rate"] for p in post_metrics]) if post_metrics else 0

    # Content type breakdown
    type_counts = {}
    type_engagement = {}
    for p in post_metrics:
        ptype = p["type"]
        type_counts[ptype] = type_counts.get(ptype, 0) + 1
        if ptype not in type_engagement:
            type_engagement[ptype] = []
        type_engagement[ptype].append(p["engagement_rate"])

    type_avg_engagement = {
        t: round(mean(rates), 2) for t, rates in type_engagement.items()
    }

    # Hashtag analysis
    hashtag_performance = {}
    for p in post_metrics:
        for tag in p.get("hashtags", []):
            if tag not in hashtag_performance:
                hashtag_performance[tag] = []
            hashtag_performance[tag].append(p["engagement_rate"])

    top_hashtags = sorted(
        [(tag, round(mean(rates), 2), len(rates)) for tag, rates in hashtag_performance.items()],
        key=lambda x: x[1], reverse=True
    )[:10]

    # Week-over-week comparison
    wow = {}
    if prev_profile:
        prev_followers = prev_profile.get("followersCount", prev_profile.get("followers", 0))
        if prev_followers > 0:
            wow["follower_change"] = followers - prev_followers
            wow["follower_change_pct"] = round((followers - prev_followers) / prev_followers * 100, 2)
    if prev_posts:
        prev_post_metrics = []
        for post in prev_posts:
            likes = post.get("likesCount", post.get("likes", 0)) or 0
            comments = post.get("commentsCount", post.get("comments", 0)) or 0
            saves = post.get("savesCount", post.get("saves", 0)) or 0
            prev_eng = likes + comments + saves
            prev_eng_rate = (prev_eng / prev_followers * 100) if prev_followers > 0 else 0
            prev_post_metrics.append(prev_eng_rate)
        if prev_post_metrics:
            prev_avg = mean(prev_post_metrics)
            wow["avg_engagement_change"] = round(avg_eng_rate - prev_avg, 2)

    # Score (0-100)
    score = min(100, int(avg_eng_rate / 3.0 * 80))  # 3% = 80 points
    if wow.get("follower_change_pct", 0) > 0.5:
        score = min(100, score + 10)
    if len(post_metrics) >= 5:  # posting consistency bonus
        score = min(100, score + 10)

    return {
        "status": "ok",
        "followers": followers,
        "following": following,
        "total_posts": post_count,
        "posts_this_period": len(post_metrics),
        "avg_engagement_rate": round(avg_eng_rate, 2),
        "best_post": post_metrics[0] if post_metrics else None,
        "worst_post": post_metrics[-1] if post_metrics else None,
        "all_posts": post_metrics,
        "content_type_breakdown": type_counts,
        "content_type_avg_engagement": type_avg_engagement,
        "top_hashtags": [{"tag": t, "avg_eng": e, "uses": c} for t, e, c in top_hashtags],
        "week_over_week": wow,
        "health_score": score,
    }


# ─── Facebook Analysis ─────────────────────────────────────────────

def analyze_facebook(page_data, prev_page=None):
    """Analyze Facebook page performance metrics."""
    if not page_data:
        return {"status": "no_data", "message": "Facebook data not available"}

    # Handle both single page object and list of pages
    page = page_data[0] if isinstance(page_data, list) else page_data
    followers = page.get("likes", page.get("followers", 0)) or 0
    posts = page.get("posts", [])

    post_metrics = []
    for post in posts:
        reactions = post.get("reactions", post.get("likes", 0)) or 0
        comments = post.get("comments", 0) or 0
        shares = post.get("shares", 0) or 0
        engagement = reactions + comments + shares
        eng_rate = (engagement / followers * 100) if followers > 0 else 0

        post_metrics.append({
            "text": (post.get("text", "") or "")[:200],
            "type": post.get("type", "unknown"),
            "timestamp": post.get("time", post.get("timestamp", "")),
            "reactions": reactions,
            "comments": comments,
            "shares": shares,
            "total_engagement": engagement,
            "engagement_rate": round(eng_rate, 2),
        })

    post_metrics.sort(key=lambda x: x["engagement_rate"], reverse=True)
    avg_eng_rate = mean([p["engagement_rate"] for p in post_metrics]) if post_metrics else 0

    wow = {}
    if prev_page:
        prev = prev_page[0] if isinstance(prev_page, list) else prev_page
        prev_followers = prev.get("likes", prev.get("followers", 0)) or 0
        if prev_followers > 0:
            wow["follower_change"] = followers - prev_followers
            wow["follower_change_pct"] = round((followers - prev_followers) / prev_followers * 100, 2)

    score = min(100, int(avg_eng_rate / 1.0 * 80))
    if wow.get("follower_change_pct", 0) > 0.3:
        score = min(100, score + 10)
    if len(post_metrics) >= 3:
        score = min(100, score + 10)

    return {
        "status": "ok",
        "followers": followers,
        "posts_this_period": len(post_metrics),
        "avg_engagement_rate": round(avg_eng_rate, 2),
        "best_post": post_metrics[0] if post_metrics else None,
        "worst_post": post_metrics[-1] if post_metrics else None,
        "all_posts": post_metrics,
        "week_over_week": wow,
        "health_score": score,
    }


# ─── YouTube Analysis ──────────────────────────────────────────────

def analyze_youtube(channel_data, prev_channel=None):
    """Analyze YouTube channel performance metrics."""
    if not channel_data:
        return {"status": "no_data", "message": "YouTube data not available"}

    channel = channel_data[0] if isinstance(channel_data, list) else channel_data
    subscribers = channel.get("subscriberCount", channel.get("subscribers", 0)) or 0
    total_views = channel.get("viewCount", channel.get("totalViews", 0)) or 0
    videos = channel.get("videos", channel.get("recentVideos", []))

    video_metrics = []
    for video in videos:
        views = video.get("viewCount", video.get("views", 0)) or 0
        likes = video.get("likeCount", video.get("likes", 0)) or 0
        comments = video.get("commentCount", video.get("comments", 0)) or 0
        engagement = likes + comments
        eng_rate = (engagement / views * 100) if views > 0 else 0

        video_metrics.append({
            "title": video.get("title", ""),
            "url": video.get("url", ""),
            "timestamp": video.get("uploadDate", video.get("date", "")),
            "views": views,
            "likes": likes,
            "comments": comments,
            "duration": video.get("duration", ""),
            "total_engagement": engagement,
            "engagement_rate": round(eng_rate, 2),
        })

    video_metrics.sort(key=lambda x: x["engagement_rate"], reverse=True)
    avg_eng_rate = mean([v["engagement_rate"] for v in video_metrics]) if video_metrics else 0
    avg_views = mean([v["views"] for v in video_metrics]) if video_metrics else 0

    wow = {}
    if prev_channel:
        prev = prev_channel[0] if isinstance(prev_channel, list) else prev_channel
        prev_subs = prev.get("subscriberCount", prev.get("subscribers", 0)) or 0
        if prev_subs > 0:
            wow["subscriber_change"] = subscribers - prev_subs
            wow["subscriber_change_pct"] = round((subscribers - prev_subs) / prev_subs * 100, 2)

    score = min(100, int(avg_eng_rate / 5.0 * 80))
    if wow.get("subscriber_change_pct", 0) > 0.5:
        score = min(100, score + 10)
    if len(video_metrics) >= 2:
        score = min(100, score + 10)

    return {
        "status": "ok",
        "subscribers": subscribers,
        "total_views": total_views,
        "videos_this_period": len(video_metrics),
        "avg_views_per_video": round(avg_views),
        "avg_engagement_rate": round(avg_eng_rate, 2),
        "best_video": video_metrics[0] if video_metrics else None,
        "worst_video": video_metrics[-1] if video_metrics else None,
        "all_videos": video_metrics,
        "week_over_week": wow,
        "health_score": score,
    }


# ─── Google Business Profile Analysis ──────────────────────────────

def analyze_google_business(review_data, prev_review=None):
    """Analyze Google Business Profile performance."""
    if not review_data:
        return {"status": "no_data", "message": "Google Business data not available"}

    biz = review_data[0] if isinstance(review_data, list) else review_data
    rating = biz.get("totalScore", biz.get("rating", 0)) or 0
    review_count = biz.get("reviewsCount", biz.get("reviews", 0)) or 0
    reviews = biz.get("reviewsData", biz.get("recentReviews", []))

    recent_reviews = []
    for review in reviews:
        recent_reviews.append({
            "author": review.get("name", review.get("author", "Anonymous")),
            "rating": review.get("stars", review.get("rating", 0)),
            "text": (review.get("text", "") or "")[:300],
            "date": review.get("publishedAtDate", review.get("date", "")),
            "response": review.get("responseFromOwnerText", ""),
        })

    reviews_with_response = sum(1 for r in recent_reviews if r.get("response"))
    response_rate = (reviews_with_response / len(recent_reviews) * 100) if recent_reviews else 0

    wow = {}
    if prev_review:
        prev = prev_review[0] if isinstance(prev_review, list) else prev_review
        prev_count = prev.get("reviewsCount", prev.get("reviews", 0)) or 0
        wow["new_reviews"] = review_count - prev_count
        prev_rating = prev.get("totalScore", prev.get("rating", 0)) or 0
        wow["rating_change"] = round(rating - prev_rating, 2)

    score = min(100, int((rating / 5.0) * 70))
    if response_rate >= 80:
        score = min(100, score + 15)
    if wow.get("new_reviews", 0) > 0:
        score = min(100, score + 15)

    return {
        "status": "ok",
        "average_rating": rating,
        "total_reviews": review_count,
        "recent_reviews": recent_reviews,
        "response_rate": round(response_rate, 1),
        "week_over_week": wow,
        "health_score": score,
    }


# ─── Overall Score ─────────────────────────────────────────────────

def calculate_overall_score(platform_results):
    """Calculate weighted overall health score."""
    weights = {
        "instagram": 0.35,
        "facebook": 0.25,
        "youtube": 0.25,
        "google_business": 0.15,
    }

    total_weight = 0
    weighted_score = 0

    for platform, weight in weights.items():
        result = platform_results.get(platform, {})
        if result.get("status") == "ok":
            weighted_score += result["health_score"] * weight
            total_weight += weight

    if total_weight > 0:
        overall = round(weighted_score / total_weight)
    else:
        overall = 0

    if overall >= 80:
        rating = "Excellent"
    elif overall >= 60:
        rating = "Good"
    elif overall >= 40:
        rating = "Needs Attention"
    elif overall >= 20:
        rating = "Concerning"
    else:
        rating = "Critical"

    return {
        "score": overall,
        "rating": rating,
        "platform_scores": {
            p: r.get("health_score", 0)
            for p, r in platform_results.items()
            if r.get("status") == "ok"
        },
    }


# ─── Main Entry Point ─────────────────────────────────────────────

def run_analysis(data_dir, report_date=None):
    """Run full analysis pipeline."""
    if report_date is None:
        report_date = datetime.now().strftime("%Y-%m-%d")

    prev_date = (datetime.strptime(report_date, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")

    base = Path(data_dir)

    # Load current data
    ig_profile = load_json(base / f"instagram/profile_{report_date}.json")
    ig_posts = load_json(base / f"instagram/posts_{report_date}.json")
    fb_page = load_json(base / f"facebook/page_{report_date}.json")
    yt_channel = load_json(base / f"youtube/channel_{report_date}.json")
    gb_reviews = load_json(base / f"google-business/reviews_{report_date}.json")

    # Load previous week data
    prev_ig_profile = load_json(base / f"instagram/profile_{prev_date}.json")
    prev_ig_posts = load_json(base / f"instagram/posts_{prev_date}.json")
    prev_fb_page = load_json(base / f"facebook/page_{prev_date}.json")
    prev_yt_channel = load_json(base / f"youtube/channel_{prev_date}.json")
    prev_gb_reviews = load_json(base / f"google-business/reviews_{prev_date}.json")

    # Run analysis for each platform
    results = {
        "instagram": analyze_instagram(ig_profile, ig_posts, prev_ig_profile, prev_ig_posts),
        "facebook": analyze_facebook(fb_page, prev_fb_page),
        "youtube": analyze_youtube(yt_channel, prev_yt_channel),
        "google_business": analyze_google_business(gb_reviews, prev_gb_reviews),
    }

    # Calculate overall score
    overall = calculate_overall_score(results)

    report = {
        "report_date": report_date,
        "previous_date": prev_date,
        "overall_health": overall,
        "platforms": results,
        "generated_at": datetime.now().isoformat(),
    }

    # Save analysis results
    output_path = base / f"reports/analysis_{report_date}.json"
    save_json(report, str(output_path))
    print(f"Analysis saved to {output_path}")

    return report


if __name__ == "__main__":
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "social-media-data"
    report_date = sys.argv[2] if len(sys.argv) > 2 else None
    result = run_analysis(data_dir, report_date)
    print(json.dumps(result, indent=2, default=str))
