import API from "../api";
import type {Token} from "../types/api/token";

class GithubAuthService {
  async callback(code: string, state: string): Promise<Token> {
    return await API.get("/auth/github/callback?code=" + code + "&state=" + state);
  }
}

export default GithubAuthService;
