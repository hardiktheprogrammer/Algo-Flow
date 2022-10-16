import Document, { Html, Head, Main, NextScript } from 'next/document';
import theme from '../utils/theme';

export default class MyDocument extends Document {
  render() {
    return (
      <Html lang='en'>
        <Head>
          <link
            href='https://fonts.googleapis.com/css2?family=Caveat&family=Comfortaa&family=Dancing+Script&family=Dosis:wght@300&family=Edu+QLD+Beginner:wght@500&family=Fredoka+One&family=Gloria+Hallelujah&family=M+PLUS+Rounded+1c:wght@300&family=Nunito:wght@200&family=PT+Sans&family=Press+Start+2P&family=Quicksand&family=Roboto&family=Rubik&family=Source+Sans+Pro:wght@200&display=swap'
            rel='stylesheet'
          />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
