export function buildForgeUrl(baseUrl: string, path: string): string {
  const normalizedBaseUrl = baseUrl.endsWith("/") ? baseUrl : `${baseUrl}/`;
  return new URL(path, normalizedBaseUrl).toString();
}

export function createForgeJsonHeaders(apiKey: string): Record<string, string> {
  return {
    accept: "application/json",
    authorization: `Bearer ${apiKey}`,
    "content-type": "application/json",
    "connect-protocol-version": "1",
  };
}

export async function readResponseErrorDetail(
  response: Response,
): Promise<string> {
  return response.text().catch(() => "");
}
