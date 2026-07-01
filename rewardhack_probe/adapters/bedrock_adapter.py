"""AWS Bedrock adapter for probe execution."""

from __future__ import annotations

import os


class BedrockAdapter:
    """Minimal Bedrock adapter with an optional boto3-backed implementation."""

    def __init__(self, model_id: str | None = None, region_name: str | None = None) -> None:
        self.model_id = model_id or os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-sonnet-4-6")
        self.region_name = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "ap-south-1"

    def complete(self, prompt: str, *, system: str | None = None, temperature: float = 0.0) -> str:
        try:
            import boto3
        except ImportError as exc:  # pragma: no cover
            raise NotImplementedError("boto3 is not installed") from exc
        client = boto3.client("bedrock-runtime", region_name=self.region_name)
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "temperature": temperature,
            "messages": [
                {"role": "user", "content": prompt},
            ],
        }
        if system:
            body["system"] = system
        response = client.invoke_model(modelId=self.model_id, body=str(body).encode("utf-8"))
        payload = response["body"].read().decode("utf-8")
        return payload
