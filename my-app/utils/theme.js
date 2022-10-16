import { extendTheme, ThemeConfig } from '@chakra-ui/react';
import { mode } from '@chakra-ui/theme-tools';

const config = {
  initialColorMode: 'dark',
  useSystemColorMode: false
};

// const styles = {
// 	global: {
// 		'html, body': {
// 			color: '#224570',
// 			lineHeight: 'tall',

// 			fontFamily: "'Caveat','Press Start 2P', sans-serif",
// 		},
// 		a: {
// 			color: '#A5C4F3',
// 		},
// 	},
// };

const styles = {
  global: (props) => ({
    'html, body': {
      color: props.colorMode == 'dark' ? 'white' : 'black',
      lineHeight: 'tall',
      fontFamily: "'Roboto', sans-serif",
      bg: mode('white', 'black')(props)
    },
    'nav, section': {
      color: props.colorMode == 'dark' ? '#A5C4F3' : '#053078'
    },
    h1: {
      fontFamily: "'Roboto', sans-serif"
    }
  })
};

const breakpoints = {
  sm: '280px',
  md: '550px',
  lg: '960px',
  xl: '1200px'
};

const colors = {
  brand: {
    100: '#354259'
  }
};

const theme = extendTheme({ config, styles, breakpoints, colors });

export default theme;
