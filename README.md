# Shape Rush V8 — Android

Projet Capacitor pour Android à partir du gameplay **Shape Rush V8 HYPERDRIVE**, sans changement de gameplay. Inclut icônes, manifeste, workflow GitHub Actions et configuration de signature Play Store.

## Obtenir un APK test (sans installer Android Studio)

1. Créer un nouveau dépôt GitHub, ou remplacer le contenu de ton dépôt de jeu existant avec **les fichiers de ce ZIP**, en conservant le dossier `.github`.
2. Aller dans **Actions** → **Shape Rush Android (APK + AAB)** → **Run workflow**.
3. À la fin, ouvrir l'exécution puis **Artifacts** → **ShapeRush-V8-test-APK**. Dézipper et installer `app-debug.apk` sur Android.
4. Le premier build peut prendre plusieurs minutes. Un APK debug sert à tester, **pas** à publier sur Google Play.

## Obtenir un AAB signé pour Google Play

Créer une **clé d'upload** et conserver le fichier et les mots de passe hors du dépôt :

```bash
keytool -genkeypair -v -keystore shape-rush-upload.jks -alias shaperush -keyalg RSA -keysize 3072 -validity 10000
```

Encoder le fichier en Base64, par exemple sur PowerShell :

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes('shape-rush-upload.jks')) | Set-Clipboard
```

Dans **GitHub → Settings → Secrets and variables → Actions**, ajouter les quatre secrets :

- `ANDROID_KEYSTORE_BASE64` : contenu Base64 de la clé
- `ANDROID_KEYSTORE_PASSWORD` : mot de passe du keystore
- `ANDROID_KEY_ALIAS` : `shaperush` (ou l'alias choisi)
- `ANDROID_KEY_PASSWORD` : mot de passe de la clé

Relancer le workflow. Un second artifact, **ShapeRush-V8-PlayStore-AAB**, sera créé si la signature est configurée. **Ne jamais perdre la clé d'upload.** Google Play App Signing est recommandé.

## Publication Play Store : éléments à finaliser

- Choisir définitivement l'identifiant Android `com.colorgate.shaperush` **avant la première publication**. Il doit être unique sur Google Play.
- Créer un compte Play Console, une fiche en magasin (description, captures, bannière, icône), déclarer l'audience cible et remplir **Sécurité des données**, classification du contenu, accès à l'application et politique de confidentialité selon le comportement réel du jeu.
- Vérifier la conformité de la version de Capacitor/Android et le niveau d'API cible demandé par Google Play **au moment de la soumission**.
- Tester sur plusieurs tailles d'écran et téléphones, vérifier les performances et le fonctionnement du son en arrière-plan.
- Créer une piste de test interne/fermée. Les conditions de test avant la production dépendent du type de compte Play Console.
- Augmenter le `versionCode` Android à chaque nouvel AAB soumis. La première version générée par Capacitor utilise généralement `versionCode 1`.

Le jeu utilise le stockage local pour son meilleur score et la vibration du téléphone. Le code HTML fourni ne comporte pas de service de publicité, d'analytics ou de backend. **Cela ne dispense pas** de vérifier les composants Android et de renseigner les déclarations Play Console.

## En local

```bash
npm install
npx cap add android
npx cap sync android
npx cap open android
```

L'APK et l'AAB **ne sont pas précompilés dans ce ZIP** : ils sont générés par GitHub Actions.
