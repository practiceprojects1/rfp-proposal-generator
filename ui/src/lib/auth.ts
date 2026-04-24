import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails,
  CognitoUserSession,
} from 'amazon-cognito-identity-js';

const poolData = {
  UserPoolId: process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID || '',
  ClientId: process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID || '',
};

const userPool = new CognitoUserPool(poolData);

export interface AuthState {
  isAuthenticated: boolean;
  user: CognitoUser | null;
  session: CognitoUserSession | null;
  token: string | null;
}

export const authService = {
  signIn: (username: string, password: string): Promise<AuthState> => {
    return new Promise((resolve, reject) => {
      const authenticationData = {
        Username: username,
        Password: password,
      };

      const authenticationDetails = new AuthenticationDetails(authenticationData);

      const userData = {
        Username: username,
        Pool: userPool,
      };

      const cognitoUser = new CognitoUser(userData);

      cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: (session) => {
          resolve({
            isAuthenticated: true,
            user: cognitoUser,
            session,
            token: session.getIdToken().getJwtToken(),
          });
        },
        onFailure: (err) => {
          reject(err);
        },
      });
    });
  },

  signOut: () => {
    const cognitoUser = userPool.getCurrentUser();
    if (cognitoUser) {
      cognitoUser.signOut();
    }
  },

  getCurrentSession: (): Promise<CognitoUserSession | null> => {
    return new Promise((resolve) => {
      const cognitoUser = userPool.getCurrentUser();
      if (cognitoUser) {
        cognitoUser.getSession((err: Error | null, session: CognitoUserSession | null) => {
          if (err || !session || !session.isValid()) {
            resolve(null);
          } else {
            resolve(session);
          }
        });
      } else {
        resolve(null);
      }
    });
  },

  getCurrentUser: (): CognitoUser | null => {
    return userPool.getCurrentUser();
  },
};