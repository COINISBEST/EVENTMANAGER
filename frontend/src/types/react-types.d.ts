declare module 'react' {
  export interface ReactElement<P = any, T extends string | JSXElementConstructor<any> = string | JSXElementConstructor<any>> {
    type: T;
    props: P;
    key: Key | null;
  }

  export const useState: <T>(initialState: T | (() => T)) => [T, Dispatch<SetStateAction<T>>];
  export const useEffect: (effect: EffectCallback, deps?: DependencyList) => void;
  export const useContext: <T>(context: Context<T>) => T;
  export const createContext: <T>(defaultValue: T) => Context<T>;
  export const useCallback: <T extends (...args: any[]) => any>(callback: T, deps: DependencyList) => T;
  export const useMemo: <T>(factory: () => T, deps: DependencyList | undefined) => T;
  export const useRef: <T>(initialValue: T) => MutableRefObject<T>;

  export type ChangeEvent<T = Element> = {
    target: T;
    currentTarget: T;
  } & BaseSyntheticEvent;

  export type DependencyList = ReadonlyArray<any>;
  export type EffectCallback = () => (void | (() => void | undefined));
  export type SetStateAction<S> = S | ((prevState: S) => S);
  export type Dispatch<A> = (value: A) => void;

  export interface Context<T> {
    Provider: Provider<T>;
    Consumer: Consumer<T>;
    displayName?: string;
  }

  export interface Provider<T> {
    $$typeof: symbol;
    _context: Context<T>;
  }

  export interface Consumer<T> {
    $$typeof: symbol;
    _context: Context<T>;
  }

  export interface MutableRefObject<T> {
    current: T;
  }
} 